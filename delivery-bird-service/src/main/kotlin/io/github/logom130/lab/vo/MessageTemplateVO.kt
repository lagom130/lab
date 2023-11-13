package io.github.logom130.lab.vo

import java.time.LocalDateTime

data class MessageTemplateVO(
        var id: Long? = null,
        var title: String? = null,
        var content: String? = null,
        var type: Int? = null,
        var published: Boolean? = null,
        var updateTime: LocalDateTime? = null
)
