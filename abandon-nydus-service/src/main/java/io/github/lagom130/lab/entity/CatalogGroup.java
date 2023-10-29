package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@TableName("catalog_group")
public class CatalogGroup implements Serializable {

    private static final long serialVersionUID = 1L;

      private Long id;

    private Integer name;

    private String code;

    private Long pid;

    
    public Long getId() {
        return id;
    }

      public void setId(Long id) {
          this.id = id;
      }
    
    public Integer getName() {
        return name;
    }

      public void setName(Integer name) {
          this.name = name;
      }
    
    public String getCode() {
        return code;
    }

      public void setCode(String code) {
          this.code = code;
      }
    
    public Long getPid() {
        return pid;
    }

      public void setPid(Long pid) {
          this.pid = pid;
      }

    @Override
    public String toString() {
        return "CatalogGroup{" +
              "id=" + id +
                  ", name=" + name +
                  ", code=" + code +
                  ", pid=" + pid +
              "}";
    }
}
