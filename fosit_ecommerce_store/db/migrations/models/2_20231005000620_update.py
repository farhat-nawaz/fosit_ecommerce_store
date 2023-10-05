from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `products` ADD `low_stock_alert_threshold` SMALLINT NOT NULL  DEFAULT 10;
        ALTER TABLE `products` MODIFY COLUMN `price` DOUBLE NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `products` DROP COLUMN `low_stock_alert_threshold`;
        ALTER TABLE `products` MODIFY COLUMN `price` INT NOT NULL;"""
