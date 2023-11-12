package io.github.logom130.lab.service.impl;

import io.github.logom130.lab.entity.MessageTemplate;
import io.github.logom130.lab.mapper.MessageTemplateMapper;
import io.github.logom130.lab.service.IMessageTemplateService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

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

}
