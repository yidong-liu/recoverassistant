package com.intellectrecovery.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.intellectrecovery.domain.Doctor;
import com.intellectrecovery.domain.Result;
import com.intellectrecovery.domain.UserData;
import com.intellectrecovery.mapper.DoctorMapper;
import com.intellectrecovery.mapper.UserDataMapper;
import com.intellectrecovery.service.DoctorService;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

import javax.annotation.Resource;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

import static com.intellectrecovery.constant.CacheKey.TOKEN_CACHE;

@Service
public class DoctorServiceImpl extends ServiceImpl<DoctorMapper, Doctor> implements DoctorService {

    @Resource
    StringRedisTemplate stringRedisTemplate;

    @Resource
    UserDataMapper userDataMapper;

    @Override
    public Result login(String username, String password) {
        Doctor doctor = query().eq("username", username).one();
        if(doctor != null) {
            if (doctor.getPassword().equals(password)){
                String code = DigestUtils.md5DigestAsHex(username.getBytes());
                stringRedisTemplate.opsForValue().set(TOKEN_CACHE + code, username, 2, TimeUnit.HOURS);
                Map<String, Object> loginInfo = new HashMap<>();
                loginInfo.put("token", code);
                loginInfo.put("role", "doctor"); // 添加角色信息
                return Result.success("登录成功", loginInfo);
            } else {
                return Result.fail("密码错误");
            }
        } else {
            return Result.fail("登录失败");
        }
    }

    @Override
    public Result exit(String username) {
        String code = DigestUtils.md5DigestAsHex(username.getBytes());
        stringRedisTemplate.delete(TOKEN_CACHE + code);
        return Result.success("退出成功");
    }

    @Override
    public Result register(String username, String password,String name) {
        String month = new SimpleDateFormat("MM").format(new Date());
        UserData userData = userDataMapper.selectOne(new QueryWrapper<UserData>().eq("month", month));
        if(userData == null) {
            userData = new UserData(null, month, 0, 1, 0);
            userDataMapper.insert(userData);
        } else {
            userData.setDoctorNum(userData.getDoctorNum() + 1);
            userDataMapper.updateById(userData);
        }
        Doctor doctor = query().eq("username", username).one();
        if(doctor == null) {
            doctor = new Doctor();
            doctor.setUsername(username);
            doctor.setPassword(password);
            doctor.setName(name);
            save(doctor);
            return Result.success("注册成功");
        } else {
         return Result.fail("用户名已存在");
        }
    }

    @Override
    public Result changePassword(String username, String password, String newPassword) {
        Doctor doctor = query().eq("username", username).one();
        if(Objects.equals(doctor.getPassword(), password)) {
            doctor.setPassword(newPassword);
            updateById(doctor);
            return Result.success("修改成功");
        } else {
            return Result.fail("原密码错误");
        }
    }

    @Override
    public Result getDoctorByTel(String tel) {
        Doctor doctor = query().eq("tel", tel).one();
        if(doctor == null) {
            return Result.fail("未找到该用户");
        } else {
            return Result.success("查找成功", doctor);
        }
    }

    @Override
    public Result getDoctorByUsername(String username) {
        Doctor doctor = query().eq("username", username).one();
        if(doctor == null) {
            return Result.fail("未找到该用户");
        } else {
            return Result.success("查找成功", doctor);
        }
    }

    @Override
    public Result updateDoctor(Doctor doctor,String username) {
        Doctor doctor1 = query().eq("username", username).one();
        doctor.setId(doctor1.getId());
        updateById(doctor);
        return Result.success("修改成功");
    }

    @Override
    public Result removeDoctor(Doctor doctor) {
        removeById(doctor.getId());
        return Result.success("删除成功");
    }

    @Override
    public Result getAll() {
        return Result.success("获取成功", query().list());
    }

}
