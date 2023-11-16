package io.github.lagom130.lab.vo;

/**
 * @author lujc
 * @date 2023/10/25.
 */
@lombok.Data
@lombok.Builder
public class SnowFlakeMetaVO {
    private Long datacenterId;
    private Long machineId;
}
