#include 
#define KEY_LENGTH 31

main(){
  unsigned char ch;
  FILE *fpIn, *fpOut;
  int i;
  unsigned char key[KEY_LENGTH] = {0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00, 0x00,
				   0x00, 0x00, 0x00};
  // Of course, I did not use the all-0 key when generating the 7 ciphertexts above!

  fpIn = fopen("messages.txt", "r");
  fpOut = fopen("ctexts.txt", "w");

  i=0;

  while (fscanf(fpIn, "%c", &ch) != EOF) {
    fprintf(fpOut, "%02X", ch^key[i]);
    i++;
    if (i==31) {
      fprintf(fpOut, "\n");
      i=0;
      fscanf(fpIn, "%c", &ch);
    }
  }

  fclose(fpIn);
  fclose(fpOut);

  return;
}
