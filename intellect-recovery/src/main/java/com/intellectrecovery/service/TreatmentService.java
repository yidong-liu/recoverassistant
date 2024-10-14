package com.intellectrecovery.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.intellectrecovery.domain.Result;
import com.intellectrecovery.domain.Treatment;

public interface TreatmentService extends IService<Treatment> {
    Result getTreatmentSituation(int userId);
    Result getSuggestion(int userId);
    Result setTreatmentSituation(int userId, String treatSituation,int doctorId);
    Result setSuggestion(int userId, String suggestion,int doctorId);
    Result updateTreatmentSituation(String treatSituation,int id);
    Result deleteTreatmentSituation(int id);
    Result updateSuggestion(String suggestion,int id);
    Result deleteSuggestion(int id);
    Result getAllSituation(int doctorId);
    Result getAllSuggestion(int doctorId);
}
