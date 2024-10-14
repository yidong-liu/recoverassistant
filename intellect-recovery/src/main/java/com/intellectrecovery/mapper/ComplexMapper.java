package com.intellectrecovery.mapper;

import com.intellectrecovery.domain.Result;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface ComplexMapper {

    @Select("select score, time from score_history where u_id = ${uId}")
    List<Map<String, String>> getHistoryScore(int uId);

    @Insert("insert into score_history (u_id, score, time) values (${uId}, ${score}, #{time})")
    void saveScore(int uId, int score, String time);

    @Select("SELECT u.*, t.treat_situation, t.suggestion " +
            "FROM user u " +
            "LEFT JOIN treatment t ON u.id = t.user_id")
    List<Map<String, Object>> getAllUsersWithTreatmentInfo();

    @Select("SELECT u.*, t.treat_situation, t.suggestion " +
            "FROM user u " +
            "JOIN treatment t ON u.id = t.user_id " +
            "WHERE u.major_doctor = #{name}")
    List<Map<String, Object>> getUsersWithTreatmentByDoctor(@Param("name") String name, @Param("doctorId") int doctorId);


}
