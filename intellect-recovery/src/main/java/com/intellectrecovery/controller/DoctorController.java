package com.intellectrecovery.controller;

import com.intellectrecovery.domain.Doctor;
import com.intellectrecovery.domain.Result;
import com.intellectrecovery.domain.Treatment;
import com.intellectrecovery.domain.User;
import com.intellectrecovery.mapper.ComplexMapper;
import com.intellectrecovery.mapper.DoctorMapper;
import com.intellectrecovery.service.DoctorService;
import com.intellectrecovery.service.TreatmentService;
import com.intellectrecovery.service.UserService;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import static com.intellectrecovery.constant.CacheKey.TOKEN_CACHE;

@RestController
@RequestMapping("/doctor")
public class DoctorController {

    @Resource
    StringRedisTemplate stringRedisTemplate;

    @Resource
    DoctorService doctorService;

    @Resource
    TreatmentService treatmentService;

    @Resource
    UserService userService;

    @Resource
    ComplexMapper complexMapper;

    @PostMapping("/login")
    public Result login(@RequestBody Doctor doctor) {
        return doctorService.login(doctor.getUsername(), doctor.getPassword());
    }

    @DeleteMapping("/exit")
    public Result exit(@RequestBody String username) {
        return doctorService.exit(username);
    }

    @PostMapping("/register")
    public Result register(@RequestBody Doctor doctor) {
        return doctorService.register(doctor.getUsername(), doctor.getPassword(),doctor.getName());
    }

    @GetMapping("/getUser")
    public Result getDoctorByUsername(@RequestHeader("token") String token) {
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            return doctorService.getDoctorByUsername(username);
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PutMapping("/changePassword")
    public Result changePassword(@RequestBody HashMap<String, String> input, @RequestHeader("token") String token) {
        String usernameInput = input.get("username");
        String password = input.get("password");
        String newPassword = input.get("newPassword");
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            return doctorService.changePassword(username, password, newPassword);
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PatchMapping("/update")
    public Result updateDoctor(@RequestBody Doctor doctor, @RequestHeader("token") String token) {
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            return doctorService.updateDoctor(doctor, username);
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PostMapping("/setSituation")
   public Result setSituation(@RequestBody Treatment treatment, @RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
            return treatmentService.setTreatmentSituation(treatment.getUserId(),treatment.getTreatSituation(),doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PostMapping("/setSuggestion")
    public Result setSuggestions(@RequestBody Treatment treatment, @RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
            return treatmentService.setSuggestion(treatment.getUserId(),treatment.getSuggestion(),doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PostMapping("/updateSituation")
    public Result updateSituation(@RequestBody Treatment treatment){
        return treatmentService.updateTreatmentSituation(treatment.getTreatSituation(),treatment.getId());
    }

    @DeleteMapping("/deleteSituation")
    public Result deleteSituation(@RequestBody Treatment treatment){
        return treatmentService.deleteTreatmentSituation(treatment.getId());
    }

    @PostMapping("/updateSuggestion")
    public Result updateSuggestion(@RequestBody Treatment treatment){
        return treatmentService.updateSuggestion(treatment.getSuggestion(),treatment.getId());
    }

    @DeleteMapping("/deleteSuggestion")
    public Result deleteSuggestion(@RequestBody Treatment treatment){
        return treatmentService.deleteSuggestion(treatment.getId());
    }

    @GetMapping("/getAllSituation")
    public Result getAllSituation(@RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
            return treatmentService.getAllSituation(doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @GetMapping("/getAllSuggestion")
    public Result getAllSuggestion(@RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
            return treatmentService.getAllSuggestion(doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @GetMapping("/getUsers")
    public Result getUsers(@RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
        if(doctor != null) {
            return userService.getUsersByDoctorName(doctor.getName(),doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @GetMapping("/getAllUsers")
    public Result getAllUsers(@RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            return userService.getAll();
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @PatchMapping("/changeUserDoctor")
    public Result changeUserDoctor(@RequestBody User user, @RequestHeader("token") String token){
        String username = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(username != null) {
            Doctor doctor = (Doctor) doctorService.getDoctorByUsername(username).getData();
            return userService.changeDoctor(user.getId(), doctor.getId());
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }

    @GetMapping("/getUserHistoryByUserId")
    public Result getUserHistoryByUserId(@RequestParam("userId") Integer userId, @RequestHeader("token") String token){
        String doctorName = stringRedisTemplate.opsForValue().get(TOKEN_CACHE + token);
        if(doctorName != null) {
            List<Map<String, String>> historyScore = complexMapper.getHistoryScore(userId);
            return Result.success("获取成功", historyScore);
        } else {
            return new Result(403, "鉴权失败", null);
        }
    }
}
