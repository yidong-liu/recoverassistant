package com.intellectrecovery.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.intellectrecovery.domain.Treatment;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface TreatmentMapper extends BaseMapper<Treatment> {
    @Select("select * from treatment where user_id = #{uId}")
    Map<String, Object> selectByUserId(@Param("uId") int uId);

}
