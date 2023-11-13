package io.github.lagom130.lab.vo

import com.fasterxml.jackson.annotation.JsonFormat
import java.time.LocalDateTime

data class MessageTemplateVO(
        var id: Long? = null,
        var title: String? = null,
        var content: String? = null,
        var type: Int? = null,
        var published: Boolean? = null,
        @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
        var updateTime: LocalDateTime? = null
)
