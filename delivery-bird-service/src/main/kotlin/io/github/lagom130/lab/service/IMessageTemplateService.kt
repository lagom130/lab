package io.github.lagom130.lab.service;

import io.github.lagom130.lab.entity.MessageTemplate;
import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.dto.MessageTemplateDTO
import io.github.lagom130.lab.vo.MessageTemplateVO

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-11-12
 */
interface IMessageTemplateService : IService<MessageTemplate> {
    /**
     * 新增
     * @param messageTemplate
     * @return
     */
    fun addOne(dto : MessageTemplateDTO) : Long

    /**
     * 删除
     * @param id
     * @return
     */
    fun deleteOne(id : Long)

    /**
     * 更新
     * @param id
     * @param messageTemplate
     * @return
     */
    fun updateOne(id : Long, dto : MessageTemplateDTO)

    /**
     * 查询
     * @param id
     * @return
     */
    fun getOne(id : Long) : MessageTemplateVO
}
