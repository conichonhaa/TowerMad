"""Adapt the 2013 Apportable 32-bit ARM libs to the modern bionic linker
(targetSdk 24): basename-only DT_NEEDED entries, no text-relocation markers
(segments receiving them are made writable; W+E is tolerated below targetSdk 26)."""
import struct, sys
DT_NULL, DT_NEEDED, DT_STRTAB, DT_SYMBOLIC, DT_TEXTREL, DT_FLAGS = 0, 1, 5, 16, 22, 30
DF_TEXTREL = 0x4
PT_LOAD, PT_DYNAMIC, PF_X, PF_W = 1, 2, 1, 2

def patch(path):
    b = bytearray(open(path, 'rb').read())
    assert b[:4] == b'\x7fELF' and b[4] == 1 and b[5] == 1, 'expect ELF32 LE'
    phoff, = struct.unpack_from('<I', b, 28)
    phentsize, phnum = struct.unpack_from('<HH', b, 42)
    changed = []
    dyn = None
    loads = []
    for i in range(phnum):
        o = phoff + i * phentsize
        p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack_from('<8I', b, o)
        if p_type == PT_LOAD and (p_flags & PF_X) and not (p_flags & PF_W):
            struct.pack_into('<I', b, o + 24, p_flags | PF_W)
            changed.append('PT_LOAD[%d] +W' % i)
        if p_type == PT_LOAD:
            loads.append((p_vaddr, p_offset, p_filesz))
        if p_type == PT_DYNAMIC:
            dyn = (p_offset, p_filesz)
    off, size = dyn
    strtab = None
    for o in range(off, off + size, 8):
        tag, val = struct.unpack_from('<iI', b, o)
        if tag == DT_NULL:
            break
        if tag == DT_STRTAB:
            strtab = next(fo + val - va for va, fo, fs in loads if va <= val < va + fs)
    for o in range(off, off + size, 8):
        tag, val = struct.unpack_from('<iI', b, o)
        if tag == DT_NULL:
            break
        if tag == DT_NEEDED:
            # Build-tree paths ("Build/.../libv.so") are only reduced to their
            # basename by the linker for targetSdk < 23; point at the basename,
            # which is already the tail of the same string.
            name = bytes(b[strtab + val:b.index(0, strtab + val)])
            if b'/' in name:
                cut = name.rindex(b'/') + 1
                struct.pack_into('<iI', b, o, DT_NEEDED, val + cut)
                changed.append('NEEDED ' + name[cut:].decode())
        elif tag == DT_TEXTREL:
            struct.pack_into('<iI', b, o, DT_SYMBOLIC, 0)
            changed.append('DT_TEXTREL->DT_SYMBOLIC')
        elif tag == DT_FLAGS and val & DF_TEXTREL:
            struct.pack_into('<iI', b, o, DT_FLAGS, val & ~DF_TEXTREL)
            changed.append('DF_TEXTREL cleared')
    # dlopen of an absolute /system/lib path is refused by linker namespaces
    # (API 24+); load the public NDK library by name instead.
    old = b'/system/lib/libOpenSLES.so\0'
    i = b.find(old)
    if i >= 0:
        b[i:i + len(old)] = b'libOpenSLES.so'.ljust(len(old), b'\0')
        changed.append('libOpenSLES path')
    open(path, 'wb').write(b)
    print(path.split('/')[-1], ', '.join(changed))

for p in sys.argv[1:]:
    patch(p)
