package io.github.logom130.lab.dto

data class MessageTemplateDTO(
        var title: String? = null,
        var content: String? = null,
        var type: Int? = null,
        var published: Boolean? = null
)
