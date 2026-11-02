import os
import struct

ARCHIVO_TXT = "contactos.txt"
ARCHIVO_BIN = "contactos.bin"

FORMATO = "i30s15s"
TAM_REGISTRO = struct.calcsize(FORMATO)

def siguiente_id():
    """Devuelve el siguiente ID según los registros que ya hay en el archivo."""
    if not os.path.exists(ARCHIVO_TXT):
        return 1
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as f:
        return sum(1 for linea in f if linea.strip()) + 1


def pedir_contacto():
    """Pide nombre y teléfono por teclado y devuelve un diccionario."""
    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    return {"id": siguiente_id(), "nombre": nombre, "telefono": telefono}

def guardar_contacto(contacto):
    with open(ARCHIVO_TXT, "a", encoding="utf-8") as f:
        f.write(f"{contacto['id']},{contacto['nombre']},{contacto['telefono']}\n")
    print("Contacto guardado en", ARCHIVO_TXT)


def mostrar_contactos():
    if not os.path.exists(ARCHIVO_TXT):
        print("Todavía no hay contactos guardados.")
        return
    print(f"{'ID':<4} {'Nombre':<20} {'Teléfono':<12}")
    print("-" * 38)
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                id_, nombre, telefono = linea.strip().split(",")
                print(f"{id_:<4} {nombre:<20} {telefono:<12}")


def leer_contactos():
    """Lee el archivo de texto y devuelve una lista de diccionarios."""
    contactos = []
    if not os.path.exists(ARCHIVO_TXT):
        return contactos
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                id_, nombre, telefono = linea.strip().split(",")
                contactos.append({"id": int(id_), "nombre": nombre, "telefono": telefono})
    return contactos

def buscar_contacto(texto):
    encontrados = [c for c in leer_contactos() if texto.lower() in c["nombre"].lower()]
    if encontrados:
        print(f"Resultados para '{texto}':")
        for c in encontrados:
            print(f" - ID {c['id']}: {c['nombre']} ({c['telefono']})")
    else:
        print(f"No se encontró ningún contacto con '{texto}'.")


def contar_contactos():
    total = len(leer_contactos())
    print("Total de contactos guardados:", total)
    return total

def guardar_binario():
    contactos = leer_contactos()
    with open(ARCHIVO_BIN, "wb") as f:
        for c in contactos:
            f.write(struct.pack(
                FORMATO,
                c["id"],
                c["nombre"].encode("utf-8")[:30],
                c["telefono"].encode("utf-8")[:15],
            ))
    print(f"{len(contactos)} contactos guardados en {ARCHIVO_BIN} "
          f"({os.path.getsize(ARCHIVO_BIN)} bytes)")


def leer_binario():
    if not os.path.exists(ARCHIVO_BIN):
        print("Primero guarda el archivo binario (opción 5).")
        return
    print(f"{'ID':<4} {'Nombre':<20} {'Teléfono':<12}")
    print("-" * 38)
    with open(ARCHIVO_BIN, "rb") as f:
        while True:
            datos = f.read(TAM_REGISTRO)
            if not datos:
                break)
            id_, nombre, telefono = struct.unpack(FORMATO, datos)
            nombre = nombre.rstrip(b"\x00").decode("utf-8")
            telefono = telefono.rstrip(b"\x00").decode("utf-8")
            print(f"{id_:<4} {nombre:<20} {telefono:<12}")

def menu():
    while True:
        print("\n===== GESTIÓN DE CONTACTOS =====")
        print("1. Agregar contacto")
        print("2. Mostrar contactos")
        print("3. Buscar contacto por nombre")
        print("4. Contar contactos")
        print("5. Guardar contactos en archivo binario")
        print("6. Leer archivo binario")
        print("7. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            guardar_contacto(pedir_contacto())
        elif opcion == "2":
            mostrar_contactos()
        elif opcion == "3":
            buscar_contacto(input("Nombre a buscar: ").strip())
        elif opcion == "4":
            contar_contactos()
        elif opcion == "5":
            guardar_binario()
        elif opcion == "6":
            leer_binario()
        elif opcion == "7":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
