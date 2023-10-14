package io.github.lagom130.lab.abandon.order.controller;

import io.github.lagom130.lab.abandon.order.dto.OrderDto;
import io.github.lagom130.lab.abandon.order.entity.Order;
import io.github.lagom130.lab.abandon.order.globalResponse.Result;
import io.github.lagom130.lab.abandon.order.service.IOrderService;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@RestController
@RequestMapping("/order")
public class OrderController {
    private static final Logger LOGGER = LoggerFactory.getLogger(OrderController.class);
    @Resource
    IOrderService orderService;


    @PostMapping("")
    public Result<Order> create(@RequestBody OrderDto dto) {
        return new Result<Order>().success(orderService.create(dto.getUserId(), dto.getCommodityCode(), dto.getOrderCount()));

    }

    @GetMapping("/test")
    public Result<Order> test() {
        return new Result<Order>().success(orderService.get(0));

    }
}
