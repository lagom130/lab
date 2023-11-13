package io.github.logom130.lab.entity;

import com.baomidou.mybatisplus.annotation.IdType
import com.baomidou.mybatisplus.annotation.TableId
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
class MessageTemplate : Serializable {
        @TableId(type= IdType.INPUT)
        var id: Long? = null
    
        var title: String? = null
    
        var content: String? = null
    
        var type: Int? = null
    
        var published: Boolean? = null
        @Version
        var version: Long? = null
    
        var updateTime: LocalDateTime? = null
    
    override fun toString(): String {
        return "MessageTemplate{" +
        "id=" + id +
        ", title=" + title +
        ", content=" + content +
        ", type=" + type +
        ", published=" + published +
        ", version=" + version +
        ", updateTime=" + updateTime +
        "}"
    }
}
