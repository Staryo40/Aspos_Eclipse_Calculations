from eclipse_end import *
import os

def main():

    try:
        print("-----------------------------------------")
        print("=== Pilih Mode ===")
        print("1. Gerhana Matahari Detail")
        print("2. Gerhana Bulan Detail")
        print("3. Gerhana Bulan dan Matahari Detail")
        print("4. Gerhana Matahari Short")
        print("5. Gerhana Bulan Short")
        print("6. Gerhana Bulan dan Matahari Short")
        print("7. Export Gerhana Matahari (Semua dalam rentang tahun)")
        print("8. Export Gerhana Matahari (Gerhana pertama tiap tahun)")
        print("9. Export Gerhana Bulan (Semua dalam rentang tahun)")
        print("10. Export Gerhana Bulan (Gerhana pertama tiap tahun)")

        mode = int(input("Input mode: ").strip())
        print("-----------------------------------------")
        print("=== Konversi Tanggal ke Year Fraction ===")
        print("Masukkan tanggal dengan format: YYYY-MM-DD")
        print("Contoh: 2022-11-08")
        user_input = input("Masukkan tanggal: ").strip()
        print("-----------------------------------------")

        if mode == 1:
            hasil = date_to_year_fraction(user_input)
            print(f"Hasil year float untuk {user_input}: {hasil}")
            k = base_lunation_number(hasil)
            print(f"Nomor lunasi adalah {k}")

            print("\nDetermining First Solar Eclipse:")
            determine_first_solar_eclipse(k, True, True)

        elif mode == 2:
            hasil = date_to_year_fraction(user_input)
            print(f"Hasil year float untuk {user_input}: {hasil}")
            k = lunation_number(hasil, MoonPhase.FULL_MOON)
            print(f"Nomor lunasi FULL MOON adalah {k}")

            output_dir = os.path.join("output", f"lunar_eclipse_{user_input}")
            os.makedirs(output_dir, exist_ok=True)

            print("\nDetermining First Lunar Eclipse:")
            determine_first_lunar_eclipse(
                k,
                simple=True,
                display=True,
                filename=os.path.join(output_dir, "lunar_eclipse_report.png")
            )

            print("\nOutput saved to folder:")
            print(f"- {output_dir}/")

        elif mode == 3:
            hasil = date_to_year_fraction(user_input)
            print(f"Hasil year float untuk {user_input}: {hasil}")
            k = base_lunation_number(hasil)
            k_full = lunation_number(hasil, MoonPhase.FULL_MOON)
            print(f"Nomor lunasi adalah {k}")
            print(f"Nomor lunasi FULL MOON adalah {k_full}")

            print("\nDetermining First Solar Eclipse:")
            determine_first_solar_eclipse(k, True, True)

            output_dir = os.path.join("output", f"lunar_eclipse_{user_input}")
            os.makedirs(output_dir, exist_ok=True)

            print("\nDetermining First Lunar Eclipse:")
            determine_first_lunar_eclipse(
                k_full,
                simple=True,
                display=True,
                filename=os.path.join(output_dir, "lunar_eclipse_report.png")
            )

            print("\nOutput saved to folder:")
            print(f"- {output_dir}/")

        elif mode == 4:
            hasil = date_to_year_fraction(user_input)
            print(f"Hasil year float untuk {user_input}: {hasil}")
            k = base_lunation_number(hasil)
            print(f"Nomor lunasi adalah {k}")

            print("\nDetermining First Solar Eclipse:")
            determine_first_solar_eclipse(k, True, False)

        elif mode == 5:
            hasil = date_to_year_fraction(user_input)
            k = lunation_number(hasil, MoonPhase.FULL_MOON)
            print(f"Nomor lunasi FULL MOON adalah {k}")

            print("\nDetermining First Lunar Eclipse:")
            determine_first_lunar_eclipse(k, simple=True, display=False)

        elif mode == 6:
            hasil = date_to_year_fraction(user_input)
            k = base_lunation_number(hasil)
            k_full = lunation_number(hasil, MoonPhase.FULL_MOON)
            print(f"Nomor lunasi adalah {k}")
            print(f"Nomor lunasi FULL MOON adalah {k_full}")

            print("\nDetermining First Solar Eclipse:")
            determine_first_solar_eclipse(k, True, False)

            print("\nDetermining First Lunar Eclipse:")
            determine_first_lunar_eclipse(k_full, simple=True, display=False)

        elif mode == 7:
            n = int(input("Masukkan jumlah tahun: ").strip())

            start_year = int(user_input[:4])
            end_year = start_year + n - 1

            output_dir = os.path.join("output", f"solar_eclipse_all_{start_year}_{n}")
            os.makedirs(output_dir, exist_ok=True)

            records = export_solar_eclipses(user_input, n, simple=True)
            print_export_summary(records)

            plot_eclipse_timeline(
                records,
                title=f"Solar Eclipses from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "solar_eclipses_timeline.png")
            )

            plot_eclipse_type_distribution(
                records,
                title=f"All Solar Eclipse Type Distribution from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "solar_eclipse_types.png")
            )

            print("\nOutput saved to folder:")
            print(f"- {output_dir}/")

        elif mode == 8:
            n = int(input("Masukkan jumlah tahun: ").strip())

            start_year = int(user_input[:4])
            end_year = start_year + n - 1

            output_dir = os.path.join("output", f"solar_eclipse_first_{start_year}_{n}")
            os.makedirs(output_dir, exist_ok=True)

            records = export_first_solar_eclipse_per_year(user_input, n, simple=True)

            print("\n=== Gerhana Matahari Pertama Tiap Tahun ===")
            print_export_summary(records)

            plot_eclipse_timeline(
                records,
                title=f"First Solar Eclipse of Each Year ({start_year} to {end_year})",
                filename=os.path.join(output_dir, "first_solar_eclipse_timeline.png")
            )

            plot_eclipse_type_distribution(
                records,
                title=f"First Solar Eclipse Type Distribution every year from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "first_solar_eclipse_types.png")
            )

            print("\nOutput saved to folder:")
            print(f"- {output_dir}/")

        elif mode == 9:
            n = int(input("Masukkan jumlah tahun: ").strip())

            start_year = int(user_input[:4])
            end_year = start_year + n - 1

            output_dir = os.path.join("output", f"lunar_eclipse_all_{start_year}_{n}")
            os.makedirs(output_dir, exist_ok=True)

            records = export_lunar_eclipses(user_input, n)
            print_export_summary(records)

            plot_eclipse_timeline(
                records,
                title=f"Lunar Eclipses from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "lunar_eclipses_timeline.png")
            )

            plot_eclipse_type_distribution(
                records,
                title=f"All Lunar Eclipse Type Distribution from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "lunar_eclipse_types.png")
            )

            print(f"\nOutput saved to folder: {output_dir}/")

        elif mode == 10:
            n = int(input("Masukkan jumlah tahun: ").strip())

            start_year = int(user_input[:4])
            end_year = start_year + n - 1

            output_dir = os.path.join("output", f"lunar_eclipse_first_{start_year}_{n}")
            os.makedirs(output_dir, exist_ok=True)

            records = export_first_lunar_eclipse_per_year(user_input, n)

            print("\n=== Gerhana Bulan Pertama Tiap Tahun ===")
            print_export_summary(records)

            plot_eclipse_timeline(
                records,
                title=f"First Lunar Eclipse of Each Year ({start_year} to {end_year})",
                filename=os.path.join(output_dir, "first_lunar_eclipse_timeline.png")
            )

            plot_eclipse_type_distribution(
                records,
                title=f"First Lunar Eclipse Type Distribution every year from {start_year} to {end_year}",
                filename=os.path.join(output_dir, "first_lunar_eclipse_types.png")
            )

            print(f"\nOutput saved to folder: {output_dir}/")

        else:
            print("Invalid choice! Please choose between 1-10")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
