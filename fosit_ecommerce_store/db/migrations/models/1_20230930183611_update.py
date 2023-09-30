from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    CREATE TABLE IF NOT EXISTS `product_categories` (
        `id` CHAR(36) NOT NULL  PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL,
        `description` LONGTEXT,
        `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
        `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
    ) CHARACTER SET utf8mb4;

    CREATE TABLE IF NOT EXISTS `products` (
        `id` CHAR(36) NOT NULL  PRIMARY KEY,
        `category_id` CHAR(36) NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        `description` LONGTEXT,
        `price` INT NOT NULL,
        `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
        `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        CONSTRAINT `fk_products_product__a7f77cf2` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`id`) ON DELETE CASCADE,
        KEY `idx_products_categor_1b2536` (`category_id`)
    ) CHARACTER SET utf8mb4;

    CREATE TABLE IF NOT EXISTS `inventory` (
        `id` CHAR(36) NOT NULL  PRIMARY KEY,
        `product_id` CHAR(36) NOT NULL,
        `quantity_change` SMALLINT NOT NULL,
        `running_total` INT NOT NULL,
        `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
        `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        CONSTRAINT `fk_inventor_products_9ed7ff0f` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
        KEY `idx_inventory_product_060d80` (`product_id`)
    ) CHARACTER SET utf8mb4;

    CREATE TABLE IF NOT EXISTS `low_stock_alerts` (
        `id` CHAR(36) NOT NULL  PRIMARY KEY,
        `product_id` CHAR(36) NOT NULL,
        `alert_threshold` SMALLINT NOT NULL,
        `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
        `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        CONSTRAINT `fk_low_stoc_products_a8414250` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
        KEY `idx_low_stock_a_product_2c715a` (`product_id`)
    ) CHARACTER SET utf8mb4;


    CREATE TABLE IF NOT EXISTS `sales` (
        `id` CHAR(36) NOT NULL  PRIMARY KEY,
        `product_id` CHAR(36) NOT NULL,
        `quantity` SMALLINT NOT NULL,
        `total_price` INT NOT NULL,
        `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
        `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        CONSTRAINT `fk_sales_products_4114e2d2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
        KEY `idx_sales_product_56bc41` (`product_id`)
    ) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `inventory`;
        DROP TABLE IF EXISTS `low_stock_alerts`;
        DROP TABLE IF EXISTS `product_categories`;
        DROP TABLE IF EXISTS `products`;
        DROP TABLE IF EXISTS `sales`;"""
