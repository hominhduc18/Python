import os
import asyncio


TIME_ZONE = {
    "Africa/Cairo":{"Countrie": "EG", "Continent": "015"},
    "America/Argentina/Buenos_Aires":{"Countrie": "AR", "Continent": "019"},
    "America/New_York":{"Countrie": "US", "Continent": "021"},
    "Asia/Ho_Chi_Minh":{"Countrie": "VN", "Continent": "035"},
    "Asia/Seoul":{"Countrie": "KR", "Continent": "030"},
    "Asia/Shanghai":{"Countrie": "CN", "Continent": "030"},
    "Australia/Sydney":{"Countrie": "AU", "Continent": "053"},
    "Europe/Berlin":{"Countrie": "DE", "Continent": "155"},
    "Europe/Paris":{"Countrie": "FR", "Continent": "155"},
}
async def get_system_time_now() -> str:
    time_now = os.popen("date \"+%d/%m/%Y %H:%M:%S\"").read().strip('\n')
    return time_now

async def get_system_time_zone():
    time_zone = os.popen("sudo timedatectl show --va -p Timezone").read().strip('\n')
    utc = os.popen("date +%Z").read().strip('\n')
    return {"time_zone": time_zone, "utc": utc}

async def set_timezone(time_zone: str, ntp: bool = True) -> None:
    if time_zone in TIME_ZONE:
        os.popen(f"sudo timedatectl set-timezone {time_zone}")
        os.popen(f"sudo timedatectl set-ntp {ntp}")
        return True
    return False

async def main():
    print(await set_timezone("Asia/Ho_Chi_Minh"))

if __name__ == "__main__":
    asyncio.run(main())
    pass
# https://zhost.vn/docs/chay-lenh-sudo-tren-linux-khong-can-nhap-mat-khau/