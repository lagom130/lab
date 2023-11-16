package io.github.lagom130.lab.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl
import io.github.lagom130.lab.client.MetaClient
import io.github.lagom130.lab.convert.MessageTemplateConvert
import io.github.lagom130.lab.dto.MessageTemplateDTO
import io.github.lagom130.lab.entity.MessageTemplate
import io.github.lagom130.lab.mapper.MessageTemplateMapper
import io.github.lagom130.lab.service.IMessageTemplateService
import io.github.lagom130.lab.vo.MessageTemplateVO
import jakarta.annotation.Resource
import org.springframework.stereotype.Service

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-11-12
 */
@Service
open class MessageTemplateServiceImpl : ServiceImpl<MessageTemplateMapper, MessageTemplate>(), IMessageTemplateService {
    @Resource
    private lateinit var messageTemplateMapper: MessageTemplateMapper
    @Resource
    private lateinit var metaClient: MetaClient;

    override fun addOne(dto: MessageTemplateDTO): Long {
        var messageTemplate = MessageTemplateConvert.INSTANCE.dtoToEntity(dto)
        val id = metaClient.getSnowflakeId()
        messageTemplate.id = id
        this.save(messageTemplate)
        return id
    }

    override fun deleteOne(id: Long) {
        this.removeById(id)
    }

    override fun updateOne(id: Long, dto: MessageTemplateDTO) {
        var messageTemplate = MessageTemplateConvert.INSTANCE.dtoToEntity(dto, this.getById(id))
        this.updateById(messageTemplate)
    }

    override fun getOne(id: Long): MessageTemplateVO? {
        return MessageTemplateConvert.INSTANCE.entityToVO(this.getById(id))
    }
}
