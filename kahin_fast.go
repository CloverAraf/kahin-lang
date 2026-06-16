package main

/*
#cgo CFLAGS: -I/data/data/com.termux/files/usr/include/python3.11
#cgo LDFLAGS: -L/data/data/com.termux/files/usr/lib -lpython3.11
#include <Python.h>
#include <stdlib.h>

static void init_python() {
    Py_Initialize();
}

static void run_code(const char* code) {
    PyRun_SimpleString(code);
}

static void finalize_python() {
    Py_Finalize();
}
*/
import "C"
import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"unsafe"
)

var KEYWORDS = map[string]string{
	"ice_aktar":"import","tanimla":"def","eger":"if","degilse_eger":"elif",
	"degilse":"else","dondu_boyunca":"while","her_biri_icin":"for","icinde":"in",
	"dondur":"return","yazdir":"print","girdi":"input","dur":"break",
	"devam_et":"continue","sinif":"class","dene":"try","yakala":"except",
	"sonunda":"finally","firlat":"raise","sil":"del","gec":"pass",
	"olumla":"assert","kuresel":"global","yerel_degil":"nonlocal",
	"lambda":"lambda","ile":"with","yukle":"yield","as":"as",
	"dogru":"True","yanlis":"False","hic":"None",
	"uzunluk":"len","aralik":"range","tam_sayi":"int","metin":"str",
	"ondalik":"float","liste":"list","sozluk":"dict","kume":"set",
	"demet":"tuple","tur":"type","yardim":"help","mutlak":"abs",
	"sirala":"sorted","ac":"open","topla":"sum","en_buyuk":"max",
	"en_kucuk":"min","bekle":"input",
	"sistem":"os","zaman":"time","istek":"requests","arayuz":"sys",
}

func transpile(source string) string {
	// Comments
	lines := strings.Split(source, "\n")
	for i, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "//") {
			lines[i] = "#" + trimmed[2:]
		}
	}
	source = strings.Join(lines, "\n")

	// Keywords - simple word replacement
	for tr, en := range KEYWORDS {
		source = strings.ReplaceAll(source, tr, en)
	}

	return source
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Kahin v14.2 Fast")
		fmt.Println("Kullanim: ./kahin_fast <dosya.kahin>")
		return
	}

	// Read file
	data, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		fmt.Printf("Hata: %v\n", err)
		return
	}

	// Transpile
	source := string(data)
	pythonCode := transpile(source)

	// Execute
	C.init_python()
	defer C.finalize_python()

	cCode := C.CString(pythonCode)
	defer C.free(unsafe.Pointer(cCode))

	C.run_code(cCode)
}
