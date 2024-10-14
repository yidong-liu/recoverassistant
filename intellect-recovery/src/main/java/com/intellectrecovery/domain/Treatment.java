package com.intellectrecovery.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Treatment {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private Integer doctorId;
    private Integer userId;
    private String treatSituation;
    private String suggestion;
    private String userName;
    private String doctorName;
}
