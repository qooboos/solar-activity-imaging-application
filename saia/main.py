from .sdo import SDOClient, Channel
import httpx


def main():
    with httpx.Client() as http:
        http.timeout = 300
        client = SDOClient(http)
        years = client.fetch_years()
        print(years)
        months = client.fetch_months(years[2])
        print(months)
        days = client.fetch_days(years[2], months[1])
        print(days)
        file_names = client.fetch_file_info(years[2], months[1], days[12])
        file_names = [f for f in file_names if f.channel == Channel.AIA131]
        print(file_names)
        print(len(file_names))


if __name__ == "__main__":
    main()
