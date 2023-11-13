package io.github.logom130.lab.convert

import io.github.logom130.lab.dto.MessageTemplateDTO
import io.github.logom130.lab.entity.MessageTemplate
import io.github.logom130.lab.vo.MessageTemplateVO
import org.mapstruct.Mapper
import org.mapstruct.MappingTarget
import org.mapstruct.factory.Mappers

/**
 * @author lujc
 * @date 2023/11/13.
 */
@Mapper(componentModel = "spring")
interface MessageTemplateConvert {
    companion object {
        val INSTANCE = Mappers.getMapper(MessageTemplateConvert::class.java)
    }

    fun dtoToEntity(dto: MessageTemplateDTO): MessageTemplate
    fun dtoToEntity(dto: MessageTemplateDTO, @MappingTarget entity: MessageTemplate): MessageTemplate

    fun entityToVO(entity: MessageTemplate): MessageTemplateVO
}
