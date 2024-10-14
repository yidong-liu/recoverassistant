package com.intellectrecovery.interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class CORSInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        response.setHeader("Access-Control-Allow-Origin", "*");
        // 设置允许的请求方式，这里允许GET和POST方法，可以根据需要添加其他方法
        response.setHeader("Access-Control-Allow-Methods", "GET, POST,PUT,DELETE,PATCH");
        response.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization,Token");
        // 如果是OPTIONS请求，直接返回成功状态
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            response.setStatus(HttpServletResponse.SC_OK);
            return false; // No further processing is needed for a preflight request
        }
        return true;
    }
}
