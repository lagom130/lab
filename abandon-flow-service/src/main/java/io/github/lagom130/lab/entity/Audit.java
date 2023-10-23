package io.github.lagom130.lab.entity;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-23
 */
public class Audit implements Serializable {

    private static final long serialVersionUID = 1L;

    private String id;

    private String code;

    private Integer flowOrder;

    private Integer passCondition;

    private String auditId;

    private String auditUser;

    private LocalDateTime auditTime;

    private String remark;

    
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
    
    public Integer getFlowOrder() {
        return flowOrder;
    }

      public void setFlowOrder(Integer flowOrder) {
          this.flowOrder = flowOrder;
      }
    
    public Integer getPassCondition() {
        return passCondition;
    }

      public void setPassCondition(Integer passCondition) {
          this.passCondition = passCondition;
      }
    
    public String getAuditId() {
        return auditId;
    }

      public void setAuditId(String auditId) {
          this.auditId = auditId;
      }
    
    public String getAuditUser() {
        return auditUser;
    }

      public void setAuditUser(String auditUser) {
          this.auditUser = auditUser;
      }
    
    public LocalDateTime getAuditTime() {
        return auditTime;
    }

      public void setAuditTime(LocalDateTime auditTime) {
          this.auditTime = auditTime;
      }
    
    public String getRemark() {
        return remark;
    }

      public void setRemark(String remark) {
          this.remark = remark;
      }

    @Override
    public String toString() {
        return "Audit{" +
              "id=" + id +
                  ", code=" + code +
                  ", flowOrder=" + flowOrder +
                  ", passCondition=" + passCondition +
                  ", auditId=" + auditId +
                  ", auditUser=" + auditUser +
                  ", auditTime=" + auditTime +
                  ", remark=" + remark +
              "}";
    }
}
