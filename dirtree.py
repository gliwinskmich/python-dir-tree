import argparse
from collections import defaultdict
from pathlib import Path

def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def get_dir_size_and_categories(path, file_categories):
    total_size = 0
    try:
        for item in path.rglob('*'):
            if item.is_file() and not item.is_symlink():
                try:
                    size = item.stat().st_size
                    total_size += size

                    ext = item.suffix.lower()
                    if ext == '':
                        ext = 'brak rozszerzenia'
                    file_categories[ext] += 1
                except (PermissionError, FileNotFoundError):
                    continue
    except (PermissionError, FileNotFoundError):
        pass
    return total_size

def print_tree(path, prefix="", is_last=True, file_categories=None, show_files=True):
    if file_categories is None:
        file_categories = defaultdict(int)

    pointer = "└── " if is_last else "├── "

    if path.is_dir():
        dir_size = get_dir_size_and_categories(path, file_categories)
        print(f"{prefix}{pointer}[DIR] {path.name} ({format_size(dir_size)})")

        new_prefix = prefix + ("    " if is_last else "│   ")

        try:
            items = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))

            # Filtrowanie
            if not show_files:
                items = [item for item in items if item.is_dir()]

            for i, item in enumerate(items):
                is_item_last = (i == len(items) - 1)
                print_tree(item, new_prefix, is_item_last, file_categories, show_files)
        except PermissionError:
            print(f"{new_prefix}└── [Brak dostępu]")
    else:
        if show_files:  # Wyświetlamy pliki tylko w trybie szczegółowym
            try:
                file_size = path.stat().st_size
                print(f"{prefix}{pointer}{path.name} ({format_size(file_size)})")
            except (PermissionError, FileNotFoundError):
                print(f"{prefix}{pointer}{path.name} (Błąd dostępu)")

def print_detailed_tree(root_path, file_categories):
    """Wyświetla szczegółowe drzewo z plikami"""
    print("\n" + "-" * 60)
    print("Szczegółowa struktura katalogów:")
    print("-" * 60)

    try:
        items = sorted(list(root_path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            print_tree(item, prefix="", is_last=is_last, file_categories=file_categories, show_files=True)
    except PermissionError:
        print("Brak uprawnień do odczytu katalogu głównego.")

def print_summary(file_categories):
    """Wyświetla podsumowanie statystyk"""
    print("\n" + "-" * 45)
    print("Pliki wg. kategorii w całej strukturze:")
    print("-" * 45)
    sorted_categories = sorted(file_categories.items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_categories:
        print(f"  {ext:<20} : {count}")
    print("\n")

def main():
    parser = argparse.ArgumentParser(description="Struktura katalogów w formie drzewa")
    parser.add_argument(
        "sciezka",
        nargs="?",
        default=".",
        help="Ścieżka do katalogu (domyślnie: bieżący katalog)"
    )
    args = parser.parse_args()

    root_path = Path(args.sciezka)
    if not root_path.exists() or not root_path.is_dir():
        print(f"Błąd: Ścieżka '{args.sciezka}' nie istnieje lub nie jest katalogiem")
        return

    file_categories = defaultdict(int)

    # Obliczamy całkowity rozmiar i zbieramy statystyki
    total_size = get_dir_size_and_categories(root_path, file_categories)

    print("\n" + "-" * 60)
    print(f"Struktura katalogu: {root_path.resolve()}")
    print("-" * 60)

    # Wyświetlamy tylko strukturę katalogów (bez plików)
    print(f"{root_path.name} ({format_size(total_size)})")
    try:
        items = sorted(list(root_path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        # Filtrujemy tylko katalogi
        dirs_only = [item for item in items if item.is_dir()]

        for i, item in enumerate(dirs_only):
            is_last = (i == len(dirs_only) - 1)
            print_tree(item, prefix="", is_last=is_last, file_categories=file_categories, show_files=False)
    except PermissionError:
        print("Brak uprawnień do odczytu katalogu głównego.")

    # Pytanie o szczegółowe drzewo
    response = input("\nWyświetlić wszystkie pliki w drzewie? [T/n]: ").strip().lower()

    if response in ['', 't', 'tak', 'y', 'yes']:
        print_detailed_tree(root_path, file_categories)

    # Pytanie o statystykę plików
    response_stats = input("\nWyświetlić pliki wg. kategorii? [T/n]: ").strip().lower()

    if response_stats in ['', 't', 'tak', 'y', 'yes']:
        print_summary(file_categories)
    else:
        print("\n")  # Pusta linia dla czytelności

if __name__ == "__main__":
    main()
