package io.github.lagom130.lab.common.web.config

import io.github.lagom130.lab.common.web.vo.LoginUser
import io.github.lagom130.lab.common.web.utils.LoginUserUtils
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.stereotype.Component
import org.springframework.web.servlet.HandlerInterceptor
import java.util.*

@Component
class BaseIntercepter : HandlerInterceptor {
    /**
     * 请求处理前
     * @param request
     * @param response
     * @param handler
     * @return
     * @throws Exception
     */
    @Throws(Exception::class)
    override fun preHandle(request: HttpServletRequest, response: HttpServletResponse, handler: Any): Boolean {
        val userId = Optional.ofNullable(request.getHeader("user-id")).map { s: String -> s.toLong() }.orElse(null)
        val username = Optional.ofNullable(request.getHeader("user-name")).orElse(null)
        val orgId = Optional.ofNullable(request.getHeader("org-id")).map { s: String -> s.toLong() }.orElse(null)
        val orgName = Optional.ofNullable(request.getHeader("org-name")).orElse(null)
        // 获取请求头中的 单位编号 信息
        LoginUserUtils.setLoginUser(LoginUser(userId, username, orgId, orgName))
        return true
    }

    /**
     * 请求处理后
     * @param request
     * @param response
     * @param handler
     * @param ex
     * @throws Exception
     */
    @Throws(Exception::class)
    override fun afterCompletion(request: HttpServletRequest, response: HttpServletResponse, handler: Any, ex: Exception?) {

        // 请求完后，需要清空 LoginUserThreadLocal 数据
        // 避免 OOM
        LoginUserUtils.removeUser()
    }
}
