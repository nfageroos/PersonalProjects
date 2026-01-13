package hw4_2280;

public class CharTree {
	
	public char payloadChar;
	public CharTree left;
	public CharTree right;
	private static int staticCharIdx = 0;
	
	/**
	 * 
	 * @param payloadChar
	 */
	public CharTree(char payloadChar){
		this.payloadChar = payloadChar;
	}
	
	/**
	 * If '^', split into child nodes with the same string. If not, assign a payload.
	 * @param encodingString
	 */
	
	
	public CharTree(String encodingString) {
		if(staticCharIdx >= encodingString.length()) {
			return;
		}
		char current = encodingString.charAt(staticCharIdx);
		
		if(current == '^') {
			staticCharIdx++;
			left = new CharTree(encodingString);
			staticCharIdx++;
			right = new CharTree(encodingString);
			
		}
		else {
			payloadChar = current;
			
		}
	}
	
	
// ITERATIVE CONSTUCTOR	
	
/**	public CharTree(String encodingString) {
		
		if(encodingString.length() == 1) {
			this.payloadChar = encodingString.charAt(0);
			return;
			
		}
		
		
		CharTree currentRoot = this;
		Stack<CharTree> stack = new Stack<CharTree>();
		
		
		staticCharIdx = 1;
		
			while(staticCharIdx < encodingString.length()) {
				
					if(encodingString.charAt(staticCharIdx) == '^') {		
						
						currentRoot.left = new CharTree('\0');
						currentRoot = currentRoot.left;
						staticCharIdx++;
						
						//currentRoot.right;
						
						CharTree node = new CharTree('\0');
						node = currentRoot.right;
						stack.push(node);
						//staticCharIdx++;
					}
					else if(encodingString.charAt(staticCharIdx+1) == '^'){
						
						currentRoot.left = new CharTree(encodingString.charAt(staticCharIdx));
						staticCharIdx++;
						
						currentRoot.right = new CharTree('\0');
						currentRoot = currentRoot.right;
						staticCharIdx++;
					}
					else {
						currentRoot.left = new CharTree(encodingString.charAt(staticCharIdx));
						staticCharIdx++;
					
						currentRoot.right = new CharTree(encodingString.charAt(staticCharIdx));
						staticCharIdx++;
						
						
						if(staticCharIdx < encodingString.length()) {
						
						currentRoot = stack.pop();
						
						
							if(encodingString.charAt(staticCharIdx) == '^') {
								currentRoot.payloadChar = '\0';
								staticCharIdx++;
								
							}
							else{
								currentRoot.payloadChar = encodingString.charAt(staticCharIdx);
								staticCharIdx++;
							
							}
							//currentRoot = node.right;
							
							UNABLE TO KEEP POINTER THROUGH STACK
															
						}
					
					
					}
					
				}
		
				
			}
		
	
	    */



		

	
	
	/**
	 * Checks if there is a payload on the node and if not, recurses on the child nodes. If there is a payload, print that payload and the code so far.
	 * @param root
	 * @param code
	 */
	public static void printCode(CharTree root, String code) {
		if(root.payloadChar != '\0') {
			System.out.printf("%c %s%n", root.payloadChar, code);
			return;
		}
		
		printCode(root.left, code + "0");
		printCode(root.right, code + "1");
	}
	
	/**
	 * Runs through msg as an array and goes down the tree left or right depending on if the bit was a '0' or '1'.
	 * @param tree
	 * @param msg
	 */
	
	
	public static void decode(CharTree tree, String msg) {
		CharTree root = tree;
		String decoded = "";
		for(char e: msg.toCharArray()) {
			if(tree.payloadChar != '\0') {
				decoded += tree.payloadChar;
				tree = root;
			}
			if(e == '0') {
				tree = tree.left;
			}
			else if(e == '1'){
				tree = tree.right;
			}
		}
		if(tree.payloadChar != '\0') {
			decoded += tree.payloadChar;
			tree = root;
		}
		
		System.out.println(decoded);
	}
	
	
	
	
	public static void main(String[] args) {
		CharTree tree = new CharTree("^a^^!^dc^rb");
		printCode(tree, "");
		decode(tree, "10110101011101101010100");
		
	}
	
}
	

	
