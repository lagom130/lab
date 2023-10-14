package io.github.lagom130.lab.abandon.account.service;

import io.github.lagom130.lab.abandon.account.entity.Account;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.transaction.annotation.Transactional;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
public interface IAccountService extends IService<Account> {
    void debit(String userId, int money);
}
