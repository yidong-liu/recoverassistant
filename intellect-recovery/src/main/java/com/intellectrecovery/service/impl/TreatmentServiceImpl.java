package com.intellectrecovery.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.intellectrecovery.domain.Doctor;
import com.intellectrecovery.domain.Result;
import com.intellectrecovery.domain.Treatment;
import com.intellectrecovery.domain.User;
import com.intellectrecovery.mapper.DoctorMapper;
import com.intellectrecovery.mapper.TreatmentMapper;
import com.intellectrecovery.mapper.UserMapper;
import com.intellectrecovery.service.TreatmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class TreatmentServiceImpl extends ServiceImpl<TreatmentMapper, Treatment> implements TreatmentService {
    @Autowired
    private DoctorMapper doctorMapper;

    @Autowired
    private UserMapper userMapper;

    @Resource
    private TreatmentMapper treatmentMapper;

    //根据用户id获取治疗情况并返回医生的姓名
    @Override
    public Result getTreatmentSituation(int userId) {
        List<Treatment> treatments = query().eq("user_id", userId).list();
        if (treatments.isEmpty()) {
            User user = userMapper.selectById(userId);
            return Result.fail(user.getUsername()+"没有诊断情况记录");
        }
        // 获取所有相关的医生ID
        List<Integer> doctorIds = treatments.stream().map(Treatment::getDoctorId).distinct().collect(Collectors.toList());

        // 查询所有医生信息
        List<Doctor> doctors = doctorMapper.selectBatchIds(doctorIds);
        Map<Integer, String> doctorNames = doctors.stream().collect(Collectors.toMap(Doctor::getId, Doctor::getName));

        // 构建每个治疗记录的结果，包括医生的姓名
        List<Map<String, Object>> results = new ArrayList<>();
        for (Treatment treatment : treatments) {
            Map<String, Object> resultMap = new HashMap<>();
            resultMap.put("situation", treatment.getTreatSituation());
            resultMap.put("doctor", doctorNames.get(treatment.getDoctorId()));
            results.add(resultMap);
        }

        return Result.success("查询成功", results);
    }

    @Override
    //根据用户id获取意见建议并返回医生的姓名
    public Result getSuggestion(int userId) {
        List<Treatment> treatments = query().eq("user_id", userId).list();
        if (treatments.isEmpty()) {
            User user = userMapper.selectById(userId);
            return Result.fail(user.getUsername()+"没有获得过意见建议");
        }
        // 获取所有相关的医生ID
        List<Integer> doctorIds = treatments.stream().map(Treatment::getDoctorId).distinct().collect(Collectors.toList());

        // 查询所有医生信息
        List<Doctor> doctors = doctorMapper.selectBatchIds(doctorIds);
        Map<Integer, String> doctorNames = doctors.stream().collect(Collectors.toMap(Doctor::getId, Doctor::getName));

        // 构建每个治疗记录的结果，包括医生的姓名
        List<Map<String, Object>> results = new ArrayList<>();
        for (Treatment treatment : treatments) {
            Map<String, Object> resultMap = new HashMap<>();
            resultMap.put("suggestion", treatment.getSuggestion());
            resultMap.put("doctor", doctorNames.get(treatment.getDoctorId()));
            results.add(resultMap);
        }

        return Result.success("查询成功", results);
    }

    //根据用户id获取治疗情况并返回医生的姓名
    @Override
    public Result setTreatmentSituation(int userId, String treatSituation, int doctorId) {
        // 验证用户和医生是否存在
        Doctor doctor = doctorMapper.selectById(doctorId);
        User user = userMapper.selectById(userId);
        if (doctor == null) {
            return Result.fail("医生不存在");
        }
        if (user == null) {
            return Result.fail("用户不存在");
        }

        // 创建新的治疗记录
        Treatment newTreatment = new Treatment();
        newTreatment.setUserId(userId);
        newTreatment.setDoctorId(doctor.getId());
        newTreatment.setTreatSituation(treatSituation);
        newTreatment.setUserName(user.getUsername());
        newTreatment.setDoctorName(doctor.getName());

        // 保存到数据库
        boolean success = false;
        Map<String, Object> map = treatmentMapper.selectByUserId(userId);
        if (map != null) {
            int id= (int) map.get("id");
            newTreatment.setId(id);
            treatmentMapper.updateById(newTreatment);
            return Result.success("诊断情况更新成功");
        }else{
             success = this.save(newTreatment);
        }
        if (success) {
            return Result.success("诊断情况上传成功");
        } else {
            return Result.fail("诊断情况上传失败");
        }
    }

    //根据用户id获取意见建议并返回医生的姓名
    @Override
    public Result setSuggestion(int userId, String suggestion, int doctorId) {
        // 验证用户和医生是否存在
        Doctor doctor = doctorMapper.selectById(doctorId);
        User user = userMapper.selectById(userId);
        if (doctor == null) {
            return Result.fail("医生不存在");
        }
        if (user == null) {
            return Result.fail("用户不存在");
        }

        // 创建新的治疗记录
        Treatment newTreatment = new Treatment();
        newTreatment.setUserId(userId);
        newTreatment.setDoctorId(doctorId);
        newTreatment.setSuggestion(suggestion);
        newTreatment.setUserName(user.getUsername());
        newTreatment.setDoctorName(doctor.getName());

        boolean success = false;
        Map<String, Object> map = treatmentMapper.selectByUserId(userId);
        if (map != null) {
            int id= (int) map.get("id");
            newTreatment.setId(id);
            treatmentMapper.updateById(newTreatment);
            return Result.success("诊断情况更新成功");
        }else{
            success = this.save(newTreatment);
        }
        if (success) {
            return Result.success("诊断情况上传成功");
        } else {
            return Result.fail("诊断情况上传失败");
        }
    }

    @Override
    public Result updateTreatmentSituation(String treatSituation, int id) {
        Treatment treatment = query().eq("id", id).one();
        if (treatment == null) {
            return Result.fail("会话不存在");
        }
        treatment.setTreatSituation(treatSituation);
        treatmentMapper.updateById(treatment);
        return Result.success("诊断情况更新成功");
    }

    @Override
    public Result deleteTreatmentSituation(int id) {
        Treatment treatment = query().eq("id", id).one();
        if (treatment == null) {
            return Result.fail("会话不存在");
        }
        treatmentMapper.deleteById(id);
        return Result.success("诊断情况删除成功");
    }

    @Override
    public Result updateSuggestion(String suggestion, int id) {
        Treatment treatment = query().eq("id", id).one();
        if (treatment == null) {
            return Result.fail("会话不存在");
        }
        treatment.setSuggestion(suggestion);
        treatmentMapper.updateById(treatment);
        return Result.success("意见更新成功");
    }

    @Override
    public Result deleteSuggestion(int id) {
        Treatment treatment = query().eq("id", id).one();
        if (treatment == null) {
            return Result.fail("会话不存在");
        }
        treatmentMapper.deleteById(id);
        return Result.success("意见删除成功");
    }

    @Override
    public Result getAllSituation(int doctorId) {
        List<Treatment> treatments = query().eq("doctor_id", doctorId).list();
        if (treatments.isEmpty()) {
            Doctor doctor = doctorMapper.selectById(doctorId);
            return Result.fail(doctor.getName()+"没有诊断情况记录");
        }
        return Result.success("查询成功", treatments);
    }

    @Override
    public Result getAllSuggestion(int doctorId) {
        List<Treatment> treatments = query().eq("doctor_id", doctorId).list();
        if (treatments.isEmpty()) {
            Doctor doctor = doctorMapper.selectById(doctorId);
            return Result.fail(doctor.getName()+"没有意见建议记录");
        }
        return Result.success("查询成功", treatments);
    }
}
