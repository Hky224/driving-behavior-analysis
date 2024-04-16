CREATE DATABASE IF NOT EXISTS `comp4442-gp`;
USE `comp4442-gp`;

DROP TABLE IF EXISTS Records;
CREATE TABLE IF NOT EXISTS Records (
    ID                          INT             NOT NULL AUTO_INCREMENT,
    DriverID                    VARCHAR(40)     NOT NULL,
    CarPlateNumber              VARCHAR(40)     NOT NULL,
    DrivingDate                 DATETIME        NOT NULL,
    isRapidlySpeedup            DOUBLE          NOT NULL,
    isRapidlySlowdown           DOUBLE          NOT NULL,
    isNeutralSlide              DOUBLE          NOT NULL,
    isNeutralSlideFinished      DOUBLE          NOT NULL,
    neutralSlideTime            DOUBLE          NOT NULL,
    isOverspeed                 DOUBLE          NOT NULL,
    isOverspeedFinished         DOUBLE          NOT NULL,
    overspeedTime               DOUBLE          NOT NULL,
    isFatigueDriving            DOUBLE          NOT NULL,
    isHthrottleStop             DOUBLE          NOT NULL,
    isOilLeak                   DOUBLE          NOT NULL,
    PRIMARY KEY (ID)
);
DROP TABLE IF EXISTS RealTimeMonitor;
CREATE TABLE IF NOT EXISTS RealTimeMonitor(
    ID                       INT             NOT NULL AUTO_INCREMENT,
    DriverID                VARCHAR(40)     NOT NULL,
    Speed                   INT             NOT NULL,
    Time                    BIGINT          NOT NULL,
    PRIMARY KEY (ID)
)