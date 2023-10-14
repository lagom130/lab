package io.github.lagom130.lab.abandon.order.dto;

public class OrderDto {
    private String userId;
    private String commodityCode;
    private int orderCount;

    public OrderDto() {
    }

    public OrderDto(String userId, String commodityCode, int orderCount) {
        this.userId = userId;
        this.commodityCode = commodityCode;
        this.orderCount = orderCount;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getCommodityCode() {
        return commodityCode;
    }

    public void setCommodityCode(String commodityCode) {
        this.commodityCode = commodityCode;
    }

    public int getOrderCount() {
        return orderCount;
    }

    public void setOrderCount(int orderCount) {
        this.orderCount = orderCount;
    }
}
