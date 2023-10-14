package io.github.lagom130.lab.abandon.order.service.impl;

import io.github.lagom130.lab.abandon.order.client.AccountClient;
import io.github.lagom130.lab.abandon.order.client.StorageClient;
import io.github.lagom130.lab.abandon.order.entity.Order;
import io.github.lagom130.lab.abandon.order.mapper.OrderMapper;
import io.github.lagom130.lab.abandon.order.service.IOrderService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.seata.core.context.RootContext;
import io.seata.spring.annotation.GlobalTransactional;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@Service
public class OrderServiceImpl extends ServiceImpl<OrderMapper, Order> implements IOrderService {
    private static final Logger LOGGER = LoggerFactory.getLogger(OrderServiceImpl.class);
    @Resource
    private AccountClient accountClient;
    @Resource
    private StorageClient storageClient;
    @Override
    @GlobalTransactional(rollbackFor = Exception.class)
    public Order create(String userId, String commodityCode, int orderCount) {
        LOGGER.info("Order Service Begin ... xid: " + RootContext.getXID());

        // 计算订单金额
        int orderMoney = calculate(commodityCode, orderCount);

        // 从账户余额扣款
        accountClient.debit(userId, orderMoney);
        // 扣减库存
        storageClient.deduct(commodityCode, orderCount);

        Order order = new Order();

        order.setUserId(userId);
        order.setCount(orderCount);
        order.setCommodityCode(commodityCode);
        order.setMoney(orderMoney);
        this.save(order);
        throw new RuntimeException("分布式回滚测试");
//        return order;
    }

    private int calculate(String commodityId, int orderCount) {
        return 200 * orderCount;
    }
}
