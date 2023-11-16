package io.github.lagom130.lab.dto

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class MessageTemplateDTO(
        var title: String? = null,
        var content: String? = null,
        var type: Int? = null,
        var published: Boolean? = null
)
