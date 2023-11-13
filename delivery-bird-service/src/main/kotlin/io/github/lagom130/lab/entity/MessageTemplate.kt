package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.IdType
import com.baomidou.mybatisplus.annotation.TableId
import com.baomidou.mybatisplus.annotation.TableLogic
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.Version
import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 *
 * </p>
 *
 * @author lagom
 * @since 2023-11-12
 */
@TableName("message_template")
data class MessageTemplate(
    @TableId(type = IdType.INPUT)
    var id: Long? = null,
    var title: String? = null,
    var content: String? = null,
    var type: Int? = null,
    var published: Boolean? = null,
    @Version
    var version: Int? = null,
    var updateTime: LocalDateTime? = null,
    @TableLogic(value = "0", delval = "1")
    var deleted: Int = 0,
) : Serializable
