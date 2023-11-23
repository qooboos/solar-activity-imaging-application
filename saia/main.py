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
        file_names = [f for f in file_names if f.channel == Channel.AIA131 and f.resolution == 512]
        print(file_names)
        print(len(file_names))
        for img in file_names:
            print("Downloading:", img.filename)
            with open(f"images/{img.filename}", "wb") as f:
                client.download_image(img, f)


if __name__ == "__main__":
    main()
