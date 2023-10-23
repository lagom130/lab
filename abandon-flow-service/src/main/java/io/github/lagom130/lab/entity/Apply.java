package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-23
 */
public class Apply implements Serializable {

    private static final long serialVersionUID = 1L;

      private String id;

    private String code;

    private String service;

    private String type;

    private String bizDataId;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<FlowItem> flow;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> customInfo;

    private LocalDateTime applyTime;

    private String applyId;

    private String applyUser;

    private Integer status;

    
    public String getId() {
        return id;
    }

      public void setId(String id) {
          this.id = id;
      }
    
    public String getCode() {
        return code;
    }

      public void setCode(String code) {
          this.code = code;
      }
    
    public String getService() {
        return service;
    }

      public void setService(String service) {
          this.service = service;
      }
    
    public String getType() {
        return type;
    }

      public void setType(String type) {
          this.type = type;
      }
    
    public String getBizDataId() {
        return bizDataId;
    }

      public void setBizDataId(String bizDataId) {
          this.bizDataId = bizDataId;
      }

    public List<FlowItem> getFlow() {
        return flow;
    }

    public void setFlow(List<FlowItem> flow) {
        this.flow = flow;
    }

    public Map<String, Object> getCustomInfo() {
        return customInfo;
    }

    public void setCustomInfo(Map<String, Object> customInfo) {
        this.customInfo = customInfo;
    }

    public LocalDateTime getApplyTime() {
        return applyTime;
    }

      public void setApplyTime(LocalDateTime applyTime) {
          this.applyTime = applyTime;
      }
    
    public String getApplyId() {
        return applyId;
    }

      public void setApplyId(String applyId) {
          this.applyId = applyId;
      }
    
    public String getApplyUser() {
        return applyUser;
    }

      public void setApplyUser(String applyUser) {
          this.applyUser = applyUser;
      }
    
    public Integer getStatus() {
        return status;
    }

      public void setStatus(Integer status) {
          this.status = status;
      }

    @Override
    public String toString() {
        return "Apply{" +
              "id=" + id +
                  ", code=" + code +
                  ", service=" + service +
                  ", type=" + type +
                  ", bizDataId=" + bizDataId +
                  ", flow=" + flow +
                  ", customInfo=" + customInfo +
                  ", applyTime=" + applyTime +
                  ", applyId=" + applyId +
                  ", applyUser=" + applyUser +
                  ", status=" + status +
              "}";
    }
}
