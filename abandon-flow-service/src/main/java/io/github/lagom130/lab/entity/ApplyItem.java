package io.github.lagom130.lab.entity;

import java.util.List;

@lombok.Data
public class ApplyItem {
    private int auditOrder;
    private int type;

    private List<Long> auditIds;
}
