package io.github.lagom130.lab.wrapprism;

import io.netty.util.internal.StringUtil;
import io.vertx.core.AbstractVerticle;
import io.vertx.core.MultiMap;
import io.vertx.core.Promise;
import io.vertx.core.Vertx;
import io.vertx.core.impl.logging.Logger;
import io.vertx.core.impl.logging.LoggerFactory;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.handler.BodyHandler;

import java.util.Map;
import java.util.stream.Collectors;

public class MainVerticle extends AbstractVerticle {
  private static final Logger LOGGER = LoggerFactory.getLogger(MainVerticle.class);

  public static void main(String[] args) {
    Vertx.vertx().deployVerticle(new MainVerticle());
  }

  @Override
  public void start(Promise<Void> startPromise) {
    Router router = Router.router(vertx);
    router.post("/v1/apigw/oauth2/token").handler(BodyHandler.create())
      .handler(ctx -> {
        String clientId = ctx.request().getFormAttribute("client_id");
        String clientSecret = ctx.request().getFormAttribute("client_secret");
        String grantType = ctx.request().getFormAttribute("grant_type");
        String scope = ctx.request().getFormAttribute("scope");
        System.out.println("remote address="+ctx.request().remoteAddress()
          +", clientId="+clientId
          +", clientSecret="+clientSecret
          +", grantType="+grantType
          +", scope="+scope);
        JsonObject resp = JsonObject.of("refresh_token", clientId,
          "token_type", "bearer",
          "access_token", clientId+"-"+clientSecret,
          "scope", scope,
          "expires_in", "3600");
        ctx.end(resp.toString());
      });
    // 组织架构部门上报http://10.10.41.11:4399/cshjjljk/organ/register
    router.route("/cshjjljk/organ/register")
      .handler(BodyHandler.create())
      .handler(ctx -> {
        System.out.println("部门上报："+ctx.body().asString());
        ctx.response().end(JsonObject.of("code", "1", "data", JsonObject.of("cascadeguid", "org"+System.currentTimeMillis())).toString());
      });
    // 应用上报
    router.route("/cshjjljk/app/register")
      .handler(BodyHandler.create())
      .handler(ctx -> {
        System.out.println("应用上报："+ctx.body().asString());
        ctx.response().end(JsonObject.of("code", "1", "data", JsonObject.of("cascadeguid", "app"+System.currentTimeMillis(), "appkey", "app"+System.currentTimeMillis(), "appsecret", "app"+System.currentTimeMillis() )).toString());
      });
    // 申请上报
    router.route("/cshjjljk/resource/apply")
      .handler(BodyHandler.create())
      .handler(ctx -> {
        System.out.println("申请上报："+ctx.body().asString());
        ctx.response().end(JsonObject.of("code", "1", "data", JsonObject.of("cascadeguid", "apply"+System.currentTimeMillis())).toString());
      });
    // 申请附件上报
    router.route("/cshjjljk/resource/fileupload")
      .handler(BodyHandler.create())
      .handler(ctx -> {
        System.out.println("申请附件上报："+ctx.body().asString());
        ctx.response().end(JsonObject.of("code", "1", "data", JsonObject.of("cascadeguid", "applyFileUpload"+System.currentTimeMillis())).toString());
      });
    // 资源订阅
    router.route("/cshjjljk/:type/subscribe")
      .handler(BodyHandler.create())
      .handler(ctx -> {
        String type = ctx.pathParam("type");
        System.out.println(type+"资源订阅上报："+ctx.body().asString());
        JsonObject data = new JsonObject();
        data.put("cascadeguid", type+"subscribe"+System.currentTimeMillis());
        data.put("targetTableName", "aaa");
        ctx.response().end(JsonObject.of("code", "1", "data", data).toString());
      });
    router.route()
      .handler(BodyHandler.create())
      .blockingHandler(rc -> {
        JsonObject params = new JsonObject();
        JsonObject headers = new JsonObject();
        MultiMap params1 = rc.request().params();
        params1.forEach((k, v) -> params.put(k, v));
        rc.request().headers().forEach((k, v) -> headers.put(k, v));
        String requestBody = rc.body().asString();
        JsonObject jsonObject = new JsonObject();
        jsonObject.put("remoteAddress", rc.request().remoteAddress().toString());
        jsonObject.put("path", rc.request().path());
        jsonObject.put("method", rc.request().method().name());
        jsonObject.put("uri", rc.request().uri());
        jsonObject.put("absoluteURI", rc.request().absoluteURI());
        jsonObject.put("params", rc.request().params().entries().stream()
          .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (v1, v2) -> v2)));
        jsonObject.put("headers", rc.request().headers().entries().stream()
          .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, (v1, v2) -> v2)));
        jsonObject.put("requestBody", requestBody);
        JsonObject responseBody = new JsonObject();
        responseBody.put("code", rc.request().getParam("code", "200"));
        responseBody.put("request", jsonObject);
        String block = rc.request().getParam("block", "");
        System.out.println(requestBody);
        if (!StringUtil.isNullOrEmpty(block)) {
          vertx.setTimer(Long.parseLong(block), l -> rc.response()
            .setStatusCode(Integer.parseInt(rc.request().getParam("statusCode", "200")))
            .end(responseBody.toString()));
        } else {
          rc.response()
            .setStatusCode(Integer.parseInt(rc.request().getParam("statusCode", "200")))
            .end(responseBody.toString());
        }
      });
    vertx.createHttpServer().requestHandler(router).listen(4399)
      .onSuccess(hs -> System.out.println("HTTP server started on port " + hs.actualPort()))
      .onFailure(Throwable::printStackTrace);
  }
}
