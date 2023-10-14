package io.github.lagom130.lab.abandon.storage.globalResponse;

public class Result<T> {
    private int code;
    private String msg;

    private T data;

    public Result() {
    }

    public Result(int code, String msg, T data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public static Result<Object> error(int code, String msg) {
        return new Result<>(code, msg, null);
    }

    public Result<T> success(T data) {
        return new Result<>(200, "操作成功", data);
    }

    public Result<T> success() {
        return this.success(null);
    }
}
