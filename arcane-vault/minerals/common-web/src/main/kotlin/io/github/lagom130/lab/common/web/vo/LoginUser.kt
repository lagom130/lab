package io.github.lagom130.lab.common.web.vo

data class LoginUser(
        val id: Long?,
        val username: String?,
        val orgId: Long?,
        val orgName: String?,
)