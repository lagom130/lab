package io.github.lagom130.lab.abandon.account.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@TableName("account_tbl")
public class Account implements Serializable {

    private static final long serialVersionUID = 1L;

      @TableId(value = "id", type = IdType.AUTO)
      private Integer id;

    private String userId;

    private Integer money;

    
    public Integer getId() {
        return id;
    }

      public void setId(Integer id) {
          this.id = id;
      }
    
    public String getUserId() {
        return userId;
    }

      public void setUserId(String userId) {
          this.userId = userId;
      }
    
    public Integer getMoney() {
        return money;
    }

      public void setMoney(Integer money) {
          this.money = money;
      }

    @Override
    public String toString() {
        return "Account{" +
              "id=" + id +
                  ", userId=" + userId +
                  ", money=" + money +
              "}";
    }
}
