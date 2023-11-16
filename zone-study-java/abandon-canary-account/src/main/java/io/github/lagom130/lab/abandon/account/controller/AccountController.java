package io.github.lagom130.lab.abandon.account.controller;

import io.github.lagom130.lab.abandon.account.globalResponse.Result;
import io.github.lagom130.lab.abandon.account.service.IAccountService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@RestController
@RequestMapping("/account")
public class AccountController {
    @Resource
    private IAccountService accountService;

    @PostMapping("/{userId}/debit")
    public Result debit(@PathVariable("userId") String userId, @RequestParam("money") int money) {
        accountService.debit(userId, money);
        return new Result().success();
    }
}
