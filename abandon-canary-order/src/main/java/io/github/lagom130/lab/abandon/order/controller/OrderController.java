package io.github.lagom130.lab.abandon.order.controller;

import io.github.lagom130.lab.abandon.order.dto.OrderDto;
import io.github.lagom130.lab.abandon.order.entity.Order;
import io.github.lagom130.lab.abandon.order.service.IOrderService;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RestController;

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
    public Order create(@RequestBody OrderDto dto) {
        try {
            return orderService.create(dto.getUserId(), dto.getCommodityCode(), dto.getOrderCount());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;

    }

}
