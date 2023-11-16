package io.github.lagom130.lab.mapper;

import io.github.lagom130.lab.entity.Audit;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import io.github.lagom130.lab.vo.AuditDetailVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * <p>
 *  Mapper 接口
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@Mapper
public interface AuditMapper extends BaseMapper<Audit> {
    AuditDetailVo getAuditDetail(@Param("id")Long id);
    List<AuditDetailVo> getAuditDetails();

}
