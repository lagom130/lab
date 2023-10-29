package io.github.lagom130.lab.entity;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
public class Catalog implements Serializable {

    private static final long serialVersionUID = 1L;

      private Long id;

    private String name;

    private String code;

    private Long groupId;

    private Long orgId;

    private String orgName;

    private Long createUser;

    private String createUsername;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

    private Boolean released;

    private Boolean auditing;

    private String detail;

    
    public Long getId() {
        return id;
    }

      public void setId(Long id) {
          this.id = id;
      }
    
    public String getName() {
        return name;
    }

      public void setName(String name) {
          this.name = name;
      }
    
    public String getCode() {
        return code;
    }

      public void setCode(String code) {
          this.code = code;
      }
    
    public Long getGroupId() {
        return groupId;
    }

      public void setGroupId(Long groupId) {
          this.groupId = groupId;
      }
    
    public Long getOrgId() {
        return orgId;
    }

      public void setOrgId(Long orgId) {
          this.orgId = orgId;
      }
    
    public String getOrgName() {
        return orgName;
    }

      public void setOrgName(String orgName) {
          this.orgName = orgName;
      }
    
    public Long getCreateUser() {
        return createUser;
    }

      public void setCreateUser(Long createUser) {
          this.createUser = createUser;
      }
    
    public String getCreateUsername() {
        return createUsername;
    }

      public void setCreateUsername(String createUsername) {
          this.createUsername = createUsername;
      }
    
    public LocalDateTime getCreatedTime() {
        return createdTime;
    }

      public void setCreatedTime(LocalDateTime createdTime) {
          this.createdTime = createdTime;
      }
    
    public LocalDateTime getUpdatedTime() {
        return updatedTime;
    }

      public void setUpdatedTime(LocalDateTime updatedTime) {
          this.updatedTime = updatedTime;
      }
    
    public Boolean getReleased() {
        return released;
    }

      public void setReleased(Boolean released) {
          this.released = released;
      }
    
    public Boolean getAuditing() {
        return auditing;
    }

      public void setAuditing(Boolean auditing) {
          this.auditing = auditing;
      }
    
    public String getDetail() {
        return detail;
    }

      public void setDetail(String detail) {
          this.detail = detail;
      }

    @Override
    public String toString() {
        return "Catalog{" +
              "id=" + id +
                  ", name=" + name +
                  ", code=" + code +
                  ", groupId=" + groupId +
                  ", orgId=" + orgId +
                  ", orgName=" + orgName +
                  ", createUser=" + createUser +
                  ", createUsername=" + createUsername +
                  ", createdTime=" + createdTime +
                  ", updatedTime=" + updatedTime +
                  ", released=" + released +
                  ", auditing=" + auditing +
                  ", detail=" + detail +
              "}";
    }
}
