# 构建阶段 - 使用与本地环境匹配的 Node.js 版本
FROM node:20-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制前端代码
COPY frontend/ .

# 构建生产版本
RUN npm run build

# 生产阶段
FROM nginx:alpine as production-stage

# 从构建阶段复制构建好的文件
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"] 