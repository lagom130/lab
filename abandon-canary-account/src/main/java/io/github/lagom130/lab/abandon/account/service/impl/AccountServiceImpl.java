package io.github.lagom130.lab.abandon.account.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import io.github.lagom130.lab.abandon.account.entity.Account;
import io.github.lagom130.lab.abandon.account.mapper.AccountMapper;
import io.github.lagom130.lab.abandon.account.service.IAccountService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.seata.core.context.RootContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@Service
public class AccountServiceImpl extends ServiceImpl<AccountMapper, Account> implements IAccountService {
    private static final Logger LOGGER = LoggerFactory.getLogger(AccountServiceImpl.class);

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void debit(String userId, int money) throws RuntimeException{
        LOGGER.info("Account Service Begin ... xid: " + RootContext.getXID());
        LambdaQueryWrapper<Account> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.ge(Account::getUserId, userId);
        Account account = this.getOne(queryWrapper);
        if(account == null) {
            throw new RuntimeException("账号不存在");
        }
        if(account.getMoney() < money) {
            throw new RuntimeException("余额不足");
        }
        account.setMoney(account.getMoney()-money);
        this.updateById(account);
    }
}
