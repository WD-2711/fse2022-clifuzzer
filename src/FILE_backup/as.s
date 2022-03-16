	.file	"testopt.c"
	.text
	.section	.rodata
	.align 8
.LC0:
	.string	"Option -%c requires an argument.\n"
.LC1:
	.string	"Unknown option `-%c'.\n"
	.align 8
.LC2:
	.string	"Unknown option character `\\x%x'.\n"
	.align 8
.LC3:
	.string	"Unknown option `-%c'. Aborting\n"
.LC4:
	.string	"Unknown option. Aborting\n"
.LC5:
	.string	"ab:c::"
	.align 8
.LC6:
	.string	"aflag = %d, bvalue = %s, cvalue = %s\n"
.LC7:
	.string	"Non-option argument %s\n"
.LC8:
	.string	"lstat"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$208, %rsp
	movl	%edi, -196(%rbp)
	movq	%rsi, -208(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$0, -188(%rbp)
	movq	$0, -176(%rbp)
	movq	$0, -168(%rbp)
	movl	$0, opterr(%rip)
	jmp	.L2
.L13:
	cmpl	$99, -180(%rbp)
	je	.L3
	cmpl	$99, -180(%rbp)
	jg	.L4
	cmpl	$98, -180(%rbp)
	je	.L5
	cmpl	$98, -180(%rbp)
	jg	.L4
	cmpl	$63, -180(%rbp)
	je	.L6
	cmpl	$97, -180(%rbp)
	jne	.L4
	movl	$1, -188(%rbp)
	jmp	.L2
.L5:
	movq	optarg(%rip), %rax
	movq	%rax, -176(%rbp)
	jmp	.L2
.L3:
	movq	optarg(%rip), %rax
	movq	%rax, -168(%rbp)
	jmp	.L2
.L6:
	movl	optopt(%rip), %eax
	cmpl	$99, %eax
	jne	.L7
	movl	optopt(%rip), %edx
	movq	stderr(%rip), %rax
	leaq	.LC0(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
	jmp	.L8
.L7:
	call	__ctype_b_loc@PLT
	movq	(%rax), %rax
	movl	optopt(%rip), %edx
	movslq	%edx, %rdx
	addq	%rdx, %rdx
	addq	%rdx, %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	andl	$16384, %eax
	testl	%eax, %eax
	je	.L9
	movl	optopt(%rip), %edx
	movq	stderr(%rip), %rax
	leaq	.LC1(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
	jmp	.L8
.L9:
	movl	optopt(%rip), %edx
	movq	stderr(%rip), %rax
	leaq	.LC2(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
.L8:
	movl	$1, %eax
	jmp	.L17
.L4:
	call	__ctype_b_loc@PLT
	movq	(%rax), %rax
	movl	optopt(%rip), %edx
	movslq	%edx, %rdx
	addq	%rdx, %rdx
	addq	%rdx, %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	andl	$16384, %eax
	testl	%eax, %eax
	je	.L11
	movl	optopt(%rip), %edx
	movq	stderr(%rip), %rax
	leaq	.LC3(%rip), %rsi
	movq	%rax, %rdi
	movl	$0, %eax
	call	fprintf@PLT
	jmp	.L12
.L11:
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$25, %edx
	movl	$1, %esi
	leaq	.LC4(%rip), %rdi
	call	fwrite@PLT
.L12:
	call	abort@PLT
.L2:
	movq	-208(%rbp), %rcx
	movl	-196(%rbp), %eax
	leaq	.LC5(%rip), %rdx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	getopt@PLT
	movl	%eax, -180(%rbp)
	cmpl	$-1, -180(%rbp)
	jne	.L13
	movq	-168(%rbp), %rcx
	movq	-176(%rbp), %rdx
	movl	-188(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC6(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	optind(%rip), %eax
	movl	%eax, -184(%rbp)
	jmp	.L14
.L16:
	movl	-184(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-208(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	-184(%rbp), %eax
	cltq
	leaq	0(,%rax,8), %rdx
	movq	-208(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	leaq	-160(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	lstat@PLT
	cmpl	$-1, %eax
	jne	.L15
	leaq	.LC8(%rip), %rdi
	call	perror@PLT
	movl	$1, %edi
	call	exit@PLT
.L15:
	addl	$1, -184(%rbp)
.L14:
	movl	-184(%rbp), %eax
	cmpl	-196(%rbp), %eax
	jl	.L16
	movl	$0, %eax
.L17:
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L18
	call	__stack_chk_fail@PLT
.L18:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
