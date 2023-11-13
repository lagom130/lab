package io.github.logom130.lab.service.impl;

import io.github.logom130.lab.entity.MessageTemplate;
import io.github.logom130.lab.mapper.MessageTemplateMapper;
import io.github.logom130.lab.service.IMessageTemplateService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.fasterxml.jackson.databind.util.BeanUtil
import io.github.logom130.lab.convert.MessageTemplateConvert
import io.github.logom130.lab.dto.MessageTemplateDTO
import io.github.logom130.lab.vo.MessageTemplateVO
import jakarta.annotation.Resource
import org.springframework.beans.BeanUtils
import org.springframework.stereotype.Service;
import java.time.LocalDateTime
import java.util.UUID
import kotlin.random.Random

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
    private lateinit var messageTemplateMapper: MessageTemplateMapper;
    override fun addOne(dto: MessageTemplateDTO): Long {
//        var messageTemplate = MessageTemplate()
//        BeanUtils.copyProperties(dto,messageTemplate)
        var messageTemplate = MessageTemplateConvert.INSTANCE.dtoToEntity(dto)
        // TODO : use meta-service id generator
        val id = Random.nextLong()
        messageTemplate.id = id
        this.save(messageTemplate)
        return id
    }

    override fun deleteOne(id: Long) {
        this.removeById(id)
    }

    override fun updateOne(id: Long, dto: MessageTemplateDTO) {
//        var messageTemplate = this.getById(id)
//        BeanUtils.copyProperties(dto,messageTemplate)
//        messageTemplate.updateTime = LocalDateTime.now()
        var messageTemplate = MessageTemplateConvert.INSTANCE.dtoToEntity(dto, this.getById(id))
        this.updateById(messageTemplate)
    }

    override fun getOne(id: Long): MessageTemplateVO {
//        val messageTemplate = this.getById(id)
//        var vo = MessageTemplateVO()
//        BeanUtils.copyProperties(messageTemplate, vo)
//        return vo
        return MessageTemplateConvert.INSTANCE.entityToVO(this.getById(id))
    }
}
