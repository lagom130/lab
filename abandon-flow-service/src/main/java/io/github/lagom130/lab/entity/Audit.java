package io.github.lagom130.lab.entity;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@lombok.Data
public class Audit implements Serializable {

    private static final long serialVersionUID = 1L;

      private Long id;

    private Long applyId;

    private Integer auditOrder;

    private Integer type;

    private Long operatorId;

    private Boolean pass;

    private Integer remark;

    private LocalDateTime operatedTime;
}
