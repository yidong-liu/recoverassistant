package com.intellectrecovery.service.impl;

import ch.qos.logback.classic.spi.EventArgUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.intellectrecovery.domain.Doctor;
import com.intellectrecovery.domain.Result;
import com.intellectrecovery.domain.User;
import com.intellectrecovery.domain.UserData;
import com.intellectrecovery.mapper.*;
import com.intellectrecovery.service.UserService;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

import javax.annotation.Resource;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static com.intellectrecovery.constant.CacheKey.TOKEN_CACHE;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Resource
    StringRedisTemplate stringRedisTemplate;

    @Resource
    UserDataMapper userDataMapper;

    @Resource
    ComplexMapper complexMapper;

    @Resource
    DoctorMapper doctorMapper;


    @Override
    public Result login(String username, String password) {
        User user = query().eq("username", username).one();
        if(user != null) {
            if (user.getPassword().equals(password)){
                String code = DigestUtils.md5DigestAsHex(username.getBytes());
                stringRedisTemplate.opsForValue().set(TOKEN_CACHE + code, username, 2, TimeUnit.HOURS);
                Map<String, Object> loginInfo = new HashMap<>();
                loginInfo.put("token", code);
                loginInfo.put("role", "user"); // 添加角色信息
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
            userData = new UserData(1, month, 1, 0, 0);
            userDataMapper.insert(userData);
        } else {
            userData.setUserNum(userData.getUserNum() + 1);
            userDataMapper.updateById(userData);
        }
        User user = query().eq("username", username).one();
        if(user == null) {
            user = new User();
            user.setUsername(username);
            user.setPassword(password);
            user.setName(name);
            save(user);
            return Result.success("注册成功");
        } else {
            return Result.fail("用户名已存在");
        }
    }

    @Override
    public Result changePassword(String username, String password, String newPassword) {
        User user = query().eq("username", username).one();
        if(Objects.equals(user.getPassword(), password)) {
            user.setPassword(newPassword);
            updateById(user);
            return Result.success("修改成功");
        } else {
            return Result.fail("原密码错误");
        }
    }

    @Override
    public Result getUserByTel(String tel) {
        User user = query().eq("tel", tel).one();
        if(user == null) {
            return Result.fail("未找到该用户");
        } else {
            return Result.success("查找成功", user);
        }
    }

    @Override
    public Result getUserByUsername(String username) {
        User user = query().eq("username", username).one();
        if(user == null) {
            return Result.fail("未找到该用户");
        } else {
            return Result.success("查找成功", user);
        }
    }

    @Override
    public Result updateUser(User user,String username) {
        User user1 = query().eq("username", username).one();
        user.setId(user1.getId());
        updateById(user);
        return Result.success("修改成功");
    }

    @Override
    public Result removeUser(User user) {
        removeById(user.getId());
        return Result.success("删除成功");
    }

    @Override
    public Result getAll() {
        List<Map<String, Object>> allUsersWithTreatmentInfo = complexMapper.getAllUsersWithTreatmentInfo();
        return Result.success("获取成功", allUsersWithTreatmentInfo);
    }

    @Override
    public Result saveScore(int uId, int score) {
        String format = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date());
        complexMapper.saveScore(uId, score, format);
        return Result.success("保存成功");
    }

    @Override
    public Result getMajorDoctor(int uId) {
        User user = query().eq("id", uId).one();
        return Result.success("获取成功",user.getMajorDoctor());
    }

    @Override
    public Result getUsersByDoctorName(String name, int doctorId) {
        List<Map<String, Object>> usersWithTreatmentByDoctor = complexMapper.getUsersWithTreatmentByDoctor(name, doctorId);
        Set<Integer> existingUserIds = usersWithTreatmentByDoctor.stream()
                .map(map -> (Integer) map.get("id"))
                .collect(Collectors.toSet());
        query().eq("major_doctor", name).list().forEach(user -> {
            if (!existingUserIds.contains(user.getId())) {
                Map<String, Object> map = new HashMap<>();
                map.put("id", user.getId());
                map.put("name", user.getName());
                map.put("tel", user.getTel());
                map.put("major_doctor", user.getMajorDoctor());
                map.put("treatment", "");
                map.put("addressProvince", user.getAddressProvince());
                map.put("addressCity", user.getAddressCity());
                map.put("addressCounty", user.getAddressCounty());
                map.put("addressDetail", user.getAddressDetail());
                map.put("birth", user.getBirth());
                map.put("suggestion","");
                usersWithTreatmentByDoctor.add(map);
                existingUserIds.add(user.getId()); // 将新添加的用户ID加入到集合中，以避免重复添加
            }
        });
        return Result.success("获取成功", usersWithTreatmentByDoctor);
    }

    @Override
    public Result changeDoctor(int uId, int dId) {
        User user = query().eq("id", uId).one();
        Doctor doctor = doctorMapper.selectById(dId);
        user.setMajorDoctor(doctor.getName());
        updateById(user);
        return Result.success("修改成功");
    }
}
