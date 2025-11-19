import time
import os
from pathlib import Path
from src.utils.create_qr.create_QR import create_qr  # адаптируй путь если нужно

def stress_test(start=100000, step_mode="double", limit=500_000, size="5"):
    """
    start — начальное количество
    step_mode — double (удвоение) или step (пошаговое)
    limit — максимальное количество вызовов
    size — размер qr для теста
    """
    n = start
    tmp_dir = Path("qr_stress_results")
    tmp_dir.mkdir(exist_ok=True)

    print(f"Старт stress-теста. Результаты будут в: {tmp_dir.resolve()}")

    while n <= limit:
        print(f"\n=== Тест {n} QR-кодов ===")

        start_time = time.time()
        success = True

        try:
            for i in range(n):
                file_path = tmp_dir / f"stress_{i}.png"
                create_qr(text=f"test_{i}", size=size, id=f"stress_{i}")
                # перемещаем результат в папку теста
                os.replace(f"resultstress_{i}.png", file_path)

        except Exception as e:
            print(f"❌ Ошибка на количестве: {n}")
            print("Ошибка:", e)
            success = False

        elapsed = time.time() - start_time

        if success:
            print(f"✅ Успех: {n} файлов, время: {elapsed:.2f} сек.")

        if not success:
            print("Останавливаем тест.")
            break

        # Увеличение нагрузки
        if step_mode == "double":
            n *= 2
        else:
            n += start

    print("\nStress-test завершён.")


if __name__ == "__main__":
    stress_test()
